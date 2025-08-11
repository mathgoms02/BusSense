import React from 'react'
import { TouchableWithoutFeedback, Keyboard, ScrollView, TouchableOpacity } from 'react-native'
import { useNavigation } from '@react-navigation/native'
import { Container, Card, Logo } from '../../components'
import { LoginButton, RegisterButton } from '~/components/molecules'
import { ForgotPasswordText, Spacer, ForgotPasswordContainer } from './styles'

export const Login = () => {
  const navigation = useNavigation()

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <ScrollView
        contentContainerStyle={{ flexGrow: 1, justifyContent: 'flex-start', alignItems: 'center' }}
        keyboardShouldPersistTaps="handled"
        style={{ backgroundColor: 'black' }} 
      >
        <Container
          align="center"
          justify="flex-start"
          bg="black"
          style={{ flex: 1, paddingTop: 64 }} 
        >
          <Logo />
          <Spacer height={30} />

          <Card
            item={{
              label: 'Nome de usuário',
              placeholder: 'Digite seu usuário',
              bg: 'white',
              secure: true,
            }}
          />

          <Spacer height={50} />

          <Card
            item={{
              label: 'Senha',
              placeholder: 'Digite sua senha',
              bg: 'white',
              secure: true,
            }}
          />

          <ForgotPasswordContainer>
            <TouchableOpacity onPress={() => {}}>
              <ForgotPasswordText>Esqueceu a senha?</ForgotPasswordText>
            </TouchableOpacity>
          </ForgotPasswordContainer>

          <LoginButton onPress={() => navigation.replace('IA')} />
          <RegisterButton onPress={() => navigation.navigate('Register')} />
        </Container>
      </ScrollView>
    </TouchableWithoutFeedback>
  )
}
