import React from 'react';
import { Line } from 'react-chartjs-2';
import { generer_dates } from '../model/generateur_dates';
import { useTranslate } from 'react-polyglot';

const jour_0 = new Date(2020, 0, 23);

export const Chart = (values) => {
    const t = useTranslate();

    const {
        recovered,
        exposed,
        infected,
        dead,
        hospitalized,
        intensive_care,
        exit_intensive_care,
    } = values;

    const lineData = {
        labels: generer_dates(jour_0, recovered.length),
        datasets: [
            {
                label: [t('chart.intensive_care')],
                data: intensive_care,
                backgroundColor: 'rgba(54, 54, 255, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.exit_intensive_care'),
                data: exit_intensive_care,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.hospitalized'),
                data: hospitalized,
                backgroundColor: 'rgba(255, 88, 132, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.dead'),
                data: dead,
                backgroundColor: 'rgba(88, 88, 88, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.infected'),
                data: infected,
                backgroundColor: 'rgba(255, 158, 132, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.recovered'),
                data: recovered,
                backgroundColor: 'rgba(88, 235, 88, 0.6)',
                borderWidth: 2,
            },
            {
                label: t('chart.exposed'),
                data: exposed,
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
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
                        text: 'Modèle SIR Complexe',
                        fontSize: 25,
                    },
                    scales: {
                        yAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Volume de population',
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
