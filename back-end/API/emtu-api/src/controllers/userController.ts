import {Request, Response} from "express";
import PasswordBcrypt from "../core/passwordBcrypt";
import tokenJWT from "../core/tokenJWT";
import { PostgresUserDataSource } from "../database/db/user/postgresUserDataSource";
import User from "../models/user";

const userDataSource = new PostgresUserDataSource();
const passwordEncrypter = new  PasswordBcrypt();

export default class UserController {
  public static async register(req: Request, res: Response): Promise<Response> {
    try {
      const { name, email, password } = req.body;

      if(!(name && email && password)){
        return res.status(400).send({
          erro:"Parâmetros inválidos"
        });
      }

      const userExists  = await userDataSource.getByEmail(email);

      if(userExists){
        return res.status(409).send({
          erro:"Usuário já existe"
        });
      }

      const encryptedPassword = await passwordEncrypter.encrypt(password);

      const user = new User(name, email, encryptedPassword);

      const createUserSuccess = await userDataSource.create(user);

      if(!createUserSuccess) return res.status(500).send({erro:"Falha ao cadastrar usuário"});

      const token = tokenJWT.create({
        "name": user.name,
        "email": user.email,
        "password": user.password
      });

      res.status(201).json({
        token: token
      });
    } catch (error) {
      return res.status(500).send({
        erro:"Falha ao cadastrar usuário"
      });
    }
  }

  public static async login(req: Request, res: Response): Promise<Response> {
    try {
      const { email, password } = req.body;

      if(!(email && password)){
        return res.status(400).send({
          erro:"Não foram enviados todos os parâmetros obrigatórios"
        });
      }

      const user  = await userDataSource.getByEmail(email);
      const isPasswordValid = user ?
        await passwordEncrypter.isValid(password, user.password)
        : null;

      if(!user || !isPasswordValid) {
        return res.status(400).send({
          erro:"Parâmetros inválidos"
        });
      };

      const userData = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
      };

      const token = tokenJWT.create(userData);

      return res.status(201).json({
        token: token
      });

    } catch (error) {
      return res.status(500).send({
        erro:"Falha ao efetuar o login do usuário"
      });
    }
  }

}