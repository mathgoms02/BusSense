import styled from 'styled-components/native'

export const RegisterContainer = styled.TouchableOpacity`
  align-items: center;
  justify-content: center;
  background-color: white;
  border-radius: ${({ theme }) => theme.metrics.px(30)}px;
  height: ${({ theme }) => theme.metrics.px(40)}px;
  width: ${({ theme }) => theme.metrics.px(270)}px;
`

export const RegisterButtonContainer = styled.View`
  flex-direction: row;
  align-items: center;
  color: white;
  justify-content: center;
  padding-bottom: ${({ theme }) => theme.metrics.px(20)}px;
`