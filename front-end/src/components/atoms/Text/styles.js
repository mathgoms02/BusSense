import styled from 'styled-components/native'

export const CustomText = styled.Text`
    font-size: ${({ theme, size }) => theme.metrics.px(size || 16)}px;
    font-weight: bold;
    margin-top: ${({ theme, mt }) => theme.metrics.px(mt || 0)}px;
`