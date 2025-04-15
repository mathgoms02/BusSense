import bcrypt from 'bcrypt';

export default class PasswordBcrypt implements IEncryption {
  async encrypt(password: string): Promise<string> {
    return await bcrypt.hash(password, 10);
  }
  
  async isValid(password: string, hash: string): Promise<boolean> {
    return await bcrypt.compare(password, hash);
  }
  
}