require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const twilio = require('twilio');
const cors = require('cors');

const app = express();
app.use(cors());
const port = process.env.PORT || 3000;

const twilioClient = twilio(process.env.TWILIO_SID, process.env.TWILIO_AUTH_TOKEN);

mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log("MongoDB Connected"))
    .catch(err => console.error(err));

const bhajanSchema = new mongoose.Schema({}, { strict: false, collection: 'daily_bhajans' });
const Bhajan = mongoose.model('Bhajans', bhajanSchema);

// The webhook that triggers the text
app.get('/trigger', async (req, res) => {
    try {
        const randomDocs = await Bhajan.aggregate([{ $sample: { size: 1 } }]);
        
        if (randomDocs.length === 0) {
            return res.status(404).send("Database is empty.");
        }

        const data = randomDocs[0];
        const textBody = `🎵 *Daily Bhajan*\n\n*Title:* ${data.Title}\n*Raga:* ${data['Ragam']}\n*Aarohana:* ${data['Ascending (Hindustani)']}\n*Avarohana:* ${data['Descending (Hindustani)']}`;

        await twilioClient.messages.create({
            from: 'whatsapp:+14155238886', 
            body: textBody,
            to: `whatsapp:${process.env.YOUR_PHONE_NUMBER}`
        });
        
        console.log(`Success: Sent details for ${data.Title}`);
        res.status(200).send("Message sent.");
    } catch (error) {
        console.error("Execution failed:", error);
        res.status(500).send("Failed to send message.");
    }
});

app.get('/api/bhajans', async (req, res) => {
    try {
        const allBhajans = await Bhajan.find({});
        res.status(200).json(allBhajans);
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch data" });
    }
});

app.listen(port, () => console.log(`Server listening on port ${port}`));