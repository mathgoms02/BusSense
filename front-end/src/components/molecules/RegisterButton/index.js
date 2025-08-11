import React from 'react'
import { RegisterContainer, RegisterButtonContainer } from './styles'
import { Text } from '~/components/atoms'


export const RegisterButton = ({ onPress }) => {
  return (
    <RegisterButtonContainer>
      <RegisterContainer onPress={onPress}>
        <Text size={16}>Cadastre-se</Text>
      </RegisterContainer>
    </RegisterButtonContainer>
  )
}
