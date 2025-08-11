import React from 'react'
import { Wrapper, Label, CardContainer, Input } from './styles'

export const Card = ({ item }) => {
  return (
    <Wrapper>
      <Label>{item.label}</Label>
      <CardContainer bg={item.bg}>
        <Input
          placeholder={item.placeholder}
          placeholderTextColor="#999"
          secureTextEntry={item.secure}
        />
      </CardContainer>
    </Wrapper>
  )
}
