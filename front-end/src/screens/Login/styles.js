import styled from 'styled-components/native'

export const Container = styled.View`
  flex: 1;
  align-items: center;
  justify-content: flex-start;
  background-color: black;
  padding-top: 64px;
`

export const Spacer = styled.View`
  height: ${({ height }) => height || 0}px;
`

export const ForgotPasswordContainer = styled.View`
  width: ${({ theme }) => theme.metrics.px(352)}px;
  margin-bottom: ${({ theme }) => theme.metrics.px(120)}px;
  margin-top: -15px;
  align-items: flex-start;
`

export const ForgotPasswordText = styled.Text`
  color: white;
  font-size: 14px;
`
