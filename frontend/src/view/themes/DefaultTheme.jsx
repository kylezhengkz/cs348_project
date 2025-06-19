import { createTheme } from "@mui/material";

const DefaultTheme = createTheme({
    cssVariables: true,
    palette: {
        primary: {
            main: "rgb(158, 115, 165)",
            light: "rgb(212, 193, 215)",
            dark: "rgb(104, 70, 109)",
            borderColour: "rgb(125, 130, 139)",
        },

        onPrimary: {
            main: "rgb(255,255,255)"
        },

        onSecondary: {
            main: "rgb(255, 255, 255)"
        },

        secondary: {
            main: "rgb(203, 128, 150)",
            light: "rgb(233, 201, 210)",
            dark: "rgb(127, 52, 74)",
            invert: "rgb(0, 204, 102)",
            invertLight: "rgb(26, 255, 140)"
        },

        tertiary: {
            main: "rgb(253, 232, 233)",
            dark: "rgb(253, 232, 233)",
        },

        text: {
            primary: "#555",
        },

        background: {
            main: "rgb(255, 255, 255)",
        },

        surface: {
            main: "rgb(255, 255, 255)",
            secondary: "rgb(251, 252, 248)",
            dark: "rgb(55, 62, 73)"
        }
    },

    typography: {
        fontFamily: "Roboto, Arial, sans-serif",
    },

    transitions: {
        medium: "all 0.5s ease-in-out",
        fast: "all 0.25s ease-in-out"
    },

    bordersRadius: {
        small: "5px",
        normal: "10px"
    }
})

export default DefaultTheme;