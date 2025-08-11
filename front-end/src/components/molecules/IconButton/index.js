import React from 'react'
import { Ionicons } from '@expo/vector-icons'
import { ButtonContainer } from './styles'

export const IconButton = ({ iconName, onPress }) => {
    return (
        <ButtonContainer onPress={onPress}>
            <Ionicons
                name={iconName}
                size={theme.metrics.px(24)}
            />
        </ButtonContainer>
    )
}
