import Password from '../../src/models/password';

describe('Password validation', () => {
  test('should not accept empty password', () => {
    expect(Password.validate(null)).toBeFalsy();
  });

  test('should return false for passwords smaller than 8 chars', () => {
    let address = 'p';
    expect(Password.validate(address.repeat(7))).toBeFalsy();
  });

  test('should have at least one number', () => {
    expect(Password.validate('Test.password')).toBeFalsy;
  });

  test('should have at least one simbol', () => {
    expect(Password.validate('testPassword3')).toBeFalsy;
  });

  test('should have at least one capital letter', () => {
    expect(Password.validate('test.password3')).toBeFalsy;
  });

  test('should have at least one lowercase letter', () => {
    expect(Password.validate('TESTE.PASSWORD3')).toBeFalsy;
  });

  test('sholud accept a valid password', () => {
    expect(Password.validate('Test.Password3')).toBeTruthy;
  });
})