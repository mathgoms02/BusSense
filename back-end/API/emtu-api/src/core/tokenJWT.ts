import jwt from "jsonwebtoken";
import { UserDto } from "../dtos/userDto";

export default class tokenJWT {
  static create(userData: UserDto): string {
    return userData ? 
      jwt.sign(userData, 
        process.env.JWT_SECRET_KEY,
        {
          expiresIn: "2h",
        }
      ) : null;
  }
}
