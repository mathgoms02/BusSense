import Email from '../../src/models/email';

describe('Email validation', () => {
  test('should not accept empty email', () => {
    expect(Email.validate(null)).toBeFalsy();
  });

  test('should return false for emails bigger than 320 chars', () => {
    let address = 'a';
    expect(Email.validate(address.repeat(310) + '@emails.com')).toBeFalsy();
  });

  test('should have @', () => {
    expect(Email.validate('email.domain.com')).toBeFalsy();
  });

  test('should have username', () => {
    expect(Email.validate('@email.com')).toBeFalsy();
  });

  test('should have a domain', () => {
    expect(Email.validate('username@.com')).toBeFalsy();
  });

  test('should have username size limited to 64 chars', () => {
    let username = 'a';
    expect(Email.validate(username.repeat(65) + '@email.com')).toBeFalsy();
  });

  test('domain size should not be greater than 255 chars', () => {
    let domain = 'a'.repeat(256);
    expect(Email.validate('username@' + domain)).toBeFalsy();
  });

  test('should not have multiple @', () => {
    expect(Email.validate('test@email@domain.com')).toBeFalsy();
  });

  test('should not accept multiple dots in username', () => {
    expect(Email.validate('invalid..example@email.com')).toBeFalsy();
  });

  test('should not accept multiple dots in domain', () => {
    expect(Email.validate('invalid@..email.com')).toBeFalsy();
  });

  test('should accept a valid email address', () => {
    expect(Email.validate('valid.email@test.com')).toBeTruthy();
  }); 
})