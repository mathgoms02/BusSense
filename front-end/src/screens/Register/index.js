import React from 'react'
import { TouchableWithoutFeedback, Keyboard, ScrollView } from 'react-native'
import { Container, Card, Logo, GoBack } from '../../components'
import { SubmitButton } from '~/components/molecules'
import { Spacer } from './styles'

export const Register = () => {
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
          <GoBack />
          <Logo />
          <Spacer height={30} />
          <Card
            item={{ label: 'E-mail', placeholder: 'Digite seu e-mail', bg: 'white', secure: false }}
          />

          <Spacer height={50} />
          <Card
            item={{ label: 'Nome de usuário', placeholder: 'Digite seu usuário', bg: 'white', secure: false }}
          />

          <Spacer height={50} />
          <Card
            item={{ label: 'Senha', placeholder: 'Digite sua senha', bg: 'white', secure: true }}
          />

          <Spacer height={93} />
          <SubmitButton onPress={() => console.log('Cadastrado...')} />
        </Container>
      </ScrollView>
    </TouchableWithoutFeedback>
  )
}
