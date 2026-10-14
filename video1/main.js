// const { exec } = require("child_process");

// exec("python main.py", (error, stdout, stderr) => {
//   if (error) {
//     console.error(`Błąd: ${error.message}`);
//     return;
//   }
//   console.log(`Wynik: ${stdout}`);
// });

const http = require("http");
const fs = require("fs");
const path = require("path");
const { exec, spawn } = require("child_process");

const server = http.createServer((req, res) => {
  if (req.url === "/api" && req.method === "POST") {
    console.log("/api")
    let body = "";

    req.on("data", chunk => {
      body += chunk.toString();
    });

    req.on("end", () => {
      const data = JSON.parse(body);

      const label = data.model_label;
      const image = data.model_image;

      console.log("Label:", label);
      console.log("Image length:", image.length);

      fs.writeFileSync("data.json", JSON.stringify(image));

      const child = spawn("python", ["main.py"]);

      child.stdin.write(JSON.stringify({ image, label }) + "\n");
      console.log(JSON.stringify({ image, label }) + "\n")

      console.log("data sent to python (in theory)")

      child.stdin.end();

      let output = "";

      child.stdout.on("data", (data) => {
        output += data.toString()
      });

      child.stderr.on("data", (data) => {
        console.error("Python error:", data.toString());
      });

      child.on("close", () => {
      try {
        const parsed = JSON.parse(output);

        console.log(parsed)
      
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(parsed));
      
      } catch (e) {
        console.error("Invalid JSON from Python:", output);
      
        res.writeHead(500);
        res.end("Invalid response from Python");
      }
    });
  });

  return;
}
  if (req.url === "/saveNODE" && req.method === "POST") {
    console.log("/saveNODE")
    let body = "";

    req.on("data", chunk => {
      body += chunk.toString();
    });

    req.on("end", () => {
      try {
        let currentData = []
        if (fs.existsSync("./training/NODE/data.json")) {
          const fileContent = fs.readFileSync("./training/NODE/data.json", "utf8");
        
          if (fileContent.trim() !== "") {
            currentData = JSON.parse(fileContent);
          }
        }
      
        currentData.push(JSON.parse(body));
        fs.writeFileSync("./training/NODE/data.json", JSON.stringify(currentData, null, 2))
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({success: true}));
      }
      catch(err) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({success: false, error: err.message}));
      }
    })
    return
  }
  let filePath = "html" + (req.url === "/" ? "/index.html" : req.url); fs.readFile(filePath, (err, data) => { if (err) { res.writeHead(404); return res.end("Not found"); } let ext = path.extname(filePath); let contentType = "text/html"; if (ext === ".js") contentType = "application/javascript"; if (ext === ".css") contentType = "text/css"; res.writeHead(200, { "Content-Type": contentType }); res.end(data); });
});

server.listen(3000, () => {
  console.log("http://localhost:3000");
});