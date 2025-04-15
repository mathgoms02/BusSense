export default class User {
  public readonly name: string;
  public readonly email: string;
  public readonly password: string;

  constructor(name: string, email: string, password: string) {
    this.name = name;
    this.email = email;
    this.password = password;
  };
}