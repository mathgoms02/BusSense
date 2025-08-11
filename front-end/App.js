import 'react-native-gesture-handler'
import React from 'react'
import { ThemeProvider } from 'styled-components'
import { theme } from './src/styles'
import { Routes } from './src/routes'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Routes />
    </ThemeProvider>
  )
}
