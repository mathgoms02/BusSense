import React, { useEffect } from 'react'
import { Text, Logo, Container} from '../../components'

export const SplashScreen = ({ navigation }) => {
  useEffect(() => {
    setTimeout(() => {
      navigation.replace('Login')
    }, 800);
  }, [navigation])

  return (
    <Container align="center" justify="center">
      <Logo /> 
      <Text>BusSense</Text> 
    </Container>
  )
}
