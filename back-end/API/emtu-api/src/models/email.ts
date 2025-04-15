
class Email {
  public readonly value: string;

  private constructor(email: string) {
    this.value = email;
  }

  public static validate(email: string): boolean {
    if(!email)
      return false;

    if(email.length > 320) 
      return false;

    const emailRegex = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
    
    if(!emailRegex.test(email))
      return false;
    
    const [username, domain] = email.split('@');
    if(username.length > 64 || domain.length > 255)
      return false;

    return true;
  }
}

export default Email;