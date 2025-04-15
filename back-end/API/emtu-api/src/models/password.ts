class Password {
  public readonly value: string;

  private constructor(password: string) {
    this.value = password;
  }

  public static validate(password: string): boolean {
    if(!password)
      return false;
    
    if(password.length < 8)
      return false;
    
    const passwordRegex = new RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[*.?!@#$%^&\(\)\{\}\[\]:;<>,./~_+-=|\\])[A-Za-z\d*.?!@#$%^&\(\)\{\}\[\]:;<>,./~_+-=|\\]{8,}$/);

    if(!passwordRegex.test(password))
      return false;
    
    return true;
  }
}

export default Password;