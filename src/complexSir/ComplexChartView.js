import React from 'react';
import { Line } from 'react-chartjs-2';
import { dummyModel } from '../model/sir';
import { generer_dates } from '../model/generateur_dates';

const jour_0 = new Date(2020, 0, 23);

var tab_dates = generer_dates(jour_0, dummyModel().healthy.length);

export const Chart = (values) => {
    const { healthy, infected, removed } = values;

    const lineData = {
        labels: tab_dates,
        datasets: [
            {
                label: ['Population saine'],
                data: healthy,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderWidth: 2,
            },
            {
                label: ['Population infectée'],
                data: infected,
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
                borderWidth: 2,
            },
            {
                label: ['Population rétablie'],
                data: removed,
                backgroundColor: 'rgba(255, 88, 132, 0.6)',
                borderWidth: 2,
            },
        ],
    };

    return (
        <div className="Chart">
            <Line
                data={lineData}
                width="10"
                height="10"
                options={{
                    title: {
                        display: true,
                        text: 'Modèle SIR simple',
                        fontSize: 25,
                    },
                    scales: {
                        yAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Part de la population',
                                    fontSize: 18,
                                },
                            },
                        ],
                        xAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Temps',
                                    fontSize: 18,
                                },
                            },
                        ],
                    },
                }}
            />
        </div>
    );
};
