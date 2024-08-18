import express from "express";
import mongoose from "mongoose";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import {config} from "dotenv";
import User from './models/User.js'; // Importar o modelo de forma síncrona

const app = express();
const port = 3000;
config();

app.use(express.json());

// Rota de listagem de usuários
app.get("/", async (req, res) => {
    try {
        const users = await User.find(); // Acessar o modelo diretamente
        res.send(users);
    } catch (error) {
        res.status(500).send({message: "Erro ao buscar usuários"});
    }
});

// Private Route
app.get('/user/:id', checkToken, async (req, res) => {
    const id = req.params.id;

    // Verifica se o ID é válido
    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(400).json({msg: 'ID inválido!'});
    }

    // Busca o usuário pelo ID e exclui o campo de senha da resposta
    const user = await User.findById(id).select('-password');

    if (!user) {
        return res.status(404).json({msg: 'Usuário não encontrado!'});
    }

    res.status(200).json({user});

});

function checkToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({msg: 'Acesso negado!'})
    }
    try {
        const secret = process.env.SECRET;
        jwt.verify(token, secret);
        next();
    } catch (error) {
        console.log(error);
        res.status(400).json({msg: "Token inválido!"})
    }
}

app.post("/auth/register", async (req, res) => {
    const {name, email, password, confirm_password, photo_profile} = req.body;

    if (!name) return res.status(422).json({message: 'O nome é obrigatório'});
    if (!email) return res.status(422).json({message: 'O email é obrigatório'});
    if (!password) return res.status(422).json({message: 'A senha é obrigatória'});
    if (password !== confirm_password) return res.status(422).json({message: 'As senhas não conferem'});

    const userExists = await User.findOne({email});
    if (userExists) return res.status(422).json({msg: 'Por favor, utilize outro e-mail!'});

    const salt = await bcrypt.genSalt(12);
    const passwordHash = await bcrypt.hash(password, salt);

    const user = new User({
        name,
        email,
        password: passwordHash,
        photo_profile,
    });
    try {
        await user.save();
        res.status(201).json({msg: 'Usuário criado com sucesso', user: {name, email, photo_profile}});
    } catch (error) {
        console.log(error);
        res.status(500).json({msg: 'Aconteceu um erro no servidor, tente novamente mais tarde!'});
    }
});

// Rota para deletar um usuário
app.delete("/:id", async (req, res) => {
    try {
        const user = await User.findByIdAndDelete(req.params.id); // Acessar o modelo diretamente
        if (!user) return res.status(404).json({message: "Usuário não encontrado"});
        res.json({message: "Usuário deletado com sucesso"});
    } catch (error) {
        res.status(500).json({message: "Erro ao deletar o usuário"});
    }
});

app.post("/auth/login", async (req, res) => {
    const {email, password} = req.body;
    // validations
    if (!email) return res.status(422).json({message: 'O email é obrigatório'});
    if (!password) return res.status(422).json({message: 'A senha é obrigatória'});

    const user = await User.findOne({email: email});
    if (!user) return res.status(422).json({msg: 'Usuário não encontrado!'});

    //check if password match
    const checkPassword = await bcrypt.compare(password, user.password);
    if (!checkPassword) return res.status(422).json({msg: 'Senha inválida!'});

    try {
        const secret = process.env.SECRET;
        const token = jwt.sign({id: user._id}, secret);
        res.status(200).json({msg: 'Autenticação realizada com sucesso', token})
    } catch (error) {
        console.log(error);
        res.status(500).json({msg: 'Aconteceu um erro no servidor, tente novamente mais tarde!'});
    }
})

// Rota para atualizar um usuário
app.put("/:id", async (req, res) => {
    const {name, email, password, photo_profile} = req.body;

    try {
        const updatedData = {
            name,
            email,
            password: await bcrypt.hash(password, 12),
            photo_profile,
        };

        const user = await User.findByIdAndUpdate(req.params.id, updatedData, {new: true});
        if (!user) return res.status(404).json({message: "Usuário não encontrado"});

        res.json(user);
    } catch (error) {
        res.status(500).json({message: "Erro ao atualizar o usuário"});
    }
});

// Conexão com o MongoDB e inicialização do servidor
mongoose.connect(`mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@communitysurveillance.woeig.mongodb.net/?retryWrites=true&w=majority&appName=CommunitySurveillance`)
    .then(() => {
        app.listen(port, () => console.log(`Servidor rodando na porta ${port}`));
        console.log("Conectado ao MongoDB");
    })
    .catch(err => console.error("Erro ao conectar ao MongoDB:", err));
