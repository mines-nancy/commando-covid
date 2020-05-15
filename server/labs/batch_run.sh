#!/bin/bash
#
# Author : Bart Lamiroy (Bart.Lamiroy@univ-lorraine.fr)
#
# batch_run will run consider a file of measured data points and iteratively take the first $i of those points
# to sequentially execute the following treatments :
#
# 1. Estimate the SIR+H parameters best fitting these $i points
# 2. Generate the full model output using these fitted parameters
# 3. Predict (and measure the confidence) of points beyond the $i
# 4. Generate an animated gif of the set of curves obtained in 3.
# 5. Group all prediction data into one single .csv file
# 6. Group computed optimal parameters for each run in one single .csv file
#

out_path="newrun"
series="input_SI"
measures="labs/data/Entrees_Rea_mai_corrige_avg.csv"
variables="labs/data/default_opt_variables.json"
model="disc"
algo="least-squares"
steps=20

for i in $(seq 5 ${steps} 55);
do
    echo "Launching batch iteration ${i}" ;
    python3 -m labs.model_fit.optimise -d ${series} -i "${measures}" -v "${variables}" -m ${model} --opt ${algo} --noplot --path "${out_path}" -s datanum_$i -n $i ;
    python3 -m labs.run_simulator -o ${series} -p "${out_path}"/*datanum_${i}.json -s datarun --noplot --path "${out_path}" ;
    python3 -m labs.gaussian_processes.gp_in_practice -i "${measures}" -n $i -p "${out_path}"/datarun_"${series}"_datanum_$i.csv --silentplot --beautify --path "${out_path}" -s prediction_$i ;
    echo "Batch iteration ${i} ... done"

#    process_id=$!
#    sleep 1

done

# echo "All processes launched, waiting for ${process_id}"
# wait $process_id

convert -delay 200,1000 $(find "${out_path}" -name \*.png | sort) "${out_path}/demo.gif"

cp -- "$(find "${out_path}" -name \*_prediction_\*csv | sort | head -1)" "${out_path}/predictions.csv"

for f in $(find "${out_path}" -name \*_prediction_\*csv | sort); do
  cut "${f}" -d , -f 4,5 | paste "${out_path}/predictions.csv" - -d, > "${out_path}/tmp_predictions.csv"
  mv "${out_path}/tmp_predictions.csv" "${out_path}/predictions.csv"
done


sed 's/\("[^ .]*"\): \([0-9\.]*\)/\1/g' $(find "${out_path}" -name \*_opt.json | sort | head -1) | sed 's/[{}]//g' > "${out_path}/optimal_parameters.csv"
echo >> "${out_path}/optimal_parameters.csv"
sed 's/\("[^ .]*"\): \([0-9\.]*\)/\2/g' $(find "${out_path}" -name \*_opt.json | sort) | sed 's/[{}]//g' >> "${out_path}/optimal_parameters.csv"

{ echo "series=${series}"
  echo "measures=${measures}"
  echo "variables=${variables}"
  echo "model=${disc}"
  echo "algo=${least-squares}"
  echo "steps=${steps}"
}  > "${out_path}"/batch_parameters.txt