import styled from 'styled-components/native'

export const Wrapper = styled.View`
  margin-top: ${({ theme }) => theme.metrics.px(-30)}px;
  margin-bottom: ${({ theme }) => theme.metrics.px(20)}px;
  width: ${({ theme }) => theme.metrics.px(352)}px;
`

export const Label = styled.Text`
  font-size: ${({ theme }) => theme.metrics.px(15)}px;
  font-weight: bold;
  color: white;
  margin-bottom: ${({ theme }) => theme.metrics.px(5)}px;
`

export const CardContainer = styled.View`
  height: ${({ theme }) => theme.metrics.px(40)}px;
  border-radius: ${({ theme }) => theme.metrics.px(10)}px;
  overflow: hidden;
  background-color: ${({ bg }) => bg || 'white'};
  justify-content: center;
  padding-horizontal: ${({ theme }) => theme.metrics.px(10)}px;
`

export const Input = styled.TextInput`
  color: black;
`
