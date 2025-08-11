import React from 'react'
import { SubmitContainer, SubmitButtonContainer } from './styles'
import { Text } from '~/components/atoms'


export const SubmitButton = ({ onPress }) => {
  return (
    <SubmitButtonContainer>
      <SubmitContainer onPress={onPress}>
        <Text size={16}>Cadastrar</Text>
      </SubmitContainer>
    </SubmitButtonContainer>
  )
}
