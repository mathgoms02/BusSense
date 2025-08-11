import React from 'react'
import { LoginContainer, LoginButtonContainer } from './styles'
import { Text } from '~/components/atoms'


export const LoginButton = ({ onPress }) => {
  return (
    <LoginButtonContainer>
      <LoginContainer onPress={onPress}>
        <Text size={16}>Entrar</Text>
      </LoginContainer>
    </LoginButtonContainer>
  )
}
