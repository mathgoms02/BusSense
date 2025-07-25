import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import { Text, Logo } from '../../components'


export const SplashScreen = () => {
  return (
    <View style={styles.container}>
      <Logo /> 
      <Text>BusSense</Text> 
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
    alignItems: 'center',
    justifyContent: 'center',
  }, 
});
