app.post("/save",(req,res)=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))

  // duplicate blok
  let last = history[0]
  if(last && last.signal === req.body.signal && last.tf === req.body.tf){
    return res.json({msg:"skip"})
  }

  history.unshift({
    tf:req.body.tf,
    signal:req.body.signal,
    entry:req.body.entry,
    time:new Date().toISOString(),
    result:"WAIT"
  })

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json({msg:"saved"})
})
