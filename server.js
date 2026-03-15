const express=require("express")
const fs=require("fs")

const app=express()

app.use(express.static("."))

app.get("/signals",(req,res)=>{

const data=fs.readFileSync("./data/signals.json")

res.json(JSON.parse(data))

})

app.listen(3000)
