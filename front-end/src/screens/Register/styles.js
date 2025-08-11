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

export const ButtonView = styled.View `
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: baseline; 
  justify-content: space-between;
`;