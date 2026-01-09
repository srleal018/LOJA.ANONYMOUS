app.post("/start/:lang", (req, res) => {
  stopBot();

  let command;
  let args;

  if (req.params.lang === "js") {
    command = "node";
    args = ["bot.js"];
  } else if (req.params.lang === "python") {
    command = "python3";
    args = ["bot.py"];
  } else {
    return res.status(400).json({ error: "Linguagem inválida" });
  }

  botProcess = spawn(command, args, { cwd: BOT_DIR });

  let output = "";

  botProcess.stdout.on("data", d => output += d.toString());
  botProcess.stderr.on("data", d => output += d.toString());

  setTimeout(() => {
    res.json({ status: "bot iniciado", logs: output || "Sem saída inicial" });
  }, 1000);
});

