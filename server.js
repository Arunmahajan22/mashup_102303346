const express = require("express");
const nodemailer = require("nodemailer");
const archiver = require("archiver");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.urlencoded({ extended: true }));

// ====== YOUR GMAIL DETAILS ======
const EMAIL = "aadikantsharma@gmail.com";
const APP_PASSWORD = "mpcbkzsoprkybixl";
// =================================

app.get("/", (req, res) => {
  res.send(`
    <h2>Mashup Generator</h2>
    <form method="POST">
      Singer Name: <input name="singer" required><br><br>
      Number of Videos: <input type="number" name="videos" required><br><br>
      Duration (seconds): <input type="number" name="duration" required><br><br>
      Email: <input type="email" name="email" required><br><br>
      <button type="submit">Generate</button>
    </form>
  `);
});

app.post("/", async (req, res) => {
  const { singer, videos, duration, email } = req.body;

  if (videos <= 10 || duration <= 20) {
    return res.send("Videos must be >10 and duration >20.");
  }

  // ===== Create Dummy ZIP (for demo) =====
  const zipPath = path.join(__dirname, "mashup.zip");
  const output = fs.createWriteStream(zipPath);
  const archive = archiver("zip");

  archive.pipe(output);
  archive.append("Mashup generated successfully!", { name: "mashup.txt" });
  await archive.finalize();
  // ========================================

  // ===== Send Email =====
  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: EMAIL,
      pass: APP_PASSWORD,
    },
  });

  const mailOptions = {
    from: EMAIL,
    to: email,
    subject: "Your Mashup File",
    text: "Mashup attached.",
    attachments: [
      {
        filename: "mashup.zip",
        path: zipPath,
      },
    ],
  };

  try {
    await transporter.sendMail(mailOptions);
    res.send("Email sent successfully!");
  } catch (error) {
    res.send("Error sending email: " + error);
  }
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});
