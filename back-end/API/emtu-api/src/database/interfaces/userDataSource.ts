import User from './../../models/user';

export default interface IUserDataSource {
  getByEmail(email: string): Promise<User>;
}