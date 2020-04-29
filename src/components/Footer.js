import React from 'react';
import { AppBar, Toolbar, makeStyles, Typography } from '@material-ui/core';
import { Link } from 'react-router-dom';

const useStyles = makeStyles({
    footer: {
        height: 32,
    },
    toolbar: {
        minHeight: 32,
        display: 'flex',
        justifyContent: 'space-between',
    },
    link: {
        color: 'white',
    },
});

export const Footer = () => {
    const classes = useStyles();
    return (
        <AppBar position="relative" className={classes.footer}>
            <Toolbar classes={{ root: classes.toolbar }}>
                <Link to="/mentions-legales">
                    <Typography className={classes.link} variant="subtitle2">
                        Mentions Légales
                    </Typography>
                </Link>
                <a href="https://github.com/mines-nancy/commando-covid">
                    <Typography className={classes.link} variant="subtitle2">
                        GitHub
                    </Typography>
                </a>
            </Toolbar>
        </AppBar>
    );
};
