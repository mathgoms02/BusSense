import React, { useRef, useEffect } from 'react'
import {
  Animated,
  TouchableWithoutFeedback,
  View,
  StyleSheet,
  BackHandler,
} from 'react-native'
import { useFocusEffect } from '@react-navigation/native'
import { Container, CircleButton } from './styles'

export const IA = () => {
  const scaleAnim = useRef(new Animated.Value(1)).current
  const bars = useRef(Array.from({ length: 7 }, () => new Animated.Value(1))).current
  const barAnimations = useRef([]) // guarda referências para parar depois

  const animateBars = () => {
    barAnimations.current = bars.map((bar, index) => {
      const animate = () => {
        const randomHeight = Math.random() * 1.5 + 0.5

        const animation = Animated.timing(bar, {
          toValue: randomHeight,
          duration: 250 + Math.random() * 200,
          useNativeDriver: true,
        })

        animation.start(() => {
          // Só continua se ainda estiver animando
          if (barAnimations.current[index]) animate()
        })

        return animation
      }

      return animate()
    })
  }

  const stopBars = () => {
    barAnimations.current.forEach((anim, i) => {
      if (bars[i]) bars[i].stopAnimation(() => bars[i].setValue(1))
    })
    barAnimations.current = [] // limpa referências
  }

  const handlePress = () => {
    // Se já está animando, para
    if (barAnimations.current.length > 0) {
      stopBars()
      return
    }

    // Anima botão
    Animated.loop(
      Animated.sequence([
        Animated.timing(scaleAnim, {
          toValue: 1.1,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
      ]),
      { iterations: 3 }
    ).start(() => {
      stopBars()
    })

    animateBars()
    console.log('IA visual ligada')
  }

  useFocusEffect(
    React.useCallback(() => {
      const onBackPress = () => true
      const subscription = BackHandler.addEventListener('hardwareBackPress', onBackPress)
      return () => subscription.remove()
    }, [])
  )

  return (
    <TouchableWithoutFeedback onPress={handlePress}>
      <Container>
        <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
          <CircleButton />
        </Animated.View>

        <View style={styles.audioBarsContainer}>
          {bars.map((bar, i) => (
            <Animated.View
              key={i}
              style={[styles.bar, { transform: [{ scaleY: bar }] }]}
            />
          ))}
        </View>
      </Container>
    </TouchableWithoutFeedback>
  )
}

const styles = StyleSheet.create({
  audioBarsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'flex-end',
    marginTop: 300,
    gap: 8,
  },
  bar: {
    width: 8,
    height: 30,
    backgroundColor: 'white',
    borderRadius: 10,
  },
})