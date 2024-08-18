import mongoose from "mongoose";

const User = mongoose.model('User', {
    name: String,
    email: String,
    password: String,
    confirm_password: String,
    photo_url: String,
});

export  default  User;