import styled from 'styled-components/native'

export const GoBackContainer = styled.TouchableOpacity`
    position: absolute;
    top: ${({ theme }) => theme.metrics.px(50)}px;
    left: ${({ theme }) => theme.metrics.px(3)}px;
    z-index: 20;
`