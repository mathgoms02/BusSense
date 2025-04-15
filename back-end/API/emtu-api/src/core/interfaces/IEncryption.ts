
interface IEncryption {
  encrypt(password: string) : Promise<string>;
  isValid(password: string, hash: string) : Promise<boolean>;
}