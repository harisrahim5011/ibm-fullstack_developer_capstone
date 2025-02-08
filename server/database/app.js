import express, { raw } from 'express';
import { connect } from 'mongoose';
import { readFileSync } from 'fs';
import cors from 'cors';
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(readFileSync("dealerships.json", 'utf8'));

connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

import Reviews, { deleteMany, insertMany, find } from './review';
import { deleteMany as _deleteMany, insertMany as _insertMany, find as _find } from './dealership';
import dealership from './dealership';

try {
    deleteMany({}).then(() => {
        insertMany(reviews_data.reviews); // Changed from ['reviews'] to .reviews
    });
    _deleteMany({}).then(() => {
        _insertMany(dealerships_data.dealerships); // Changed from ['dealerships'] to .dealerships
    });
} catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
}

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const documents = await find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const documents = await find({ dealership: req.params.id });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const documents = await _find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const documents = await _find({ state: req.params.state });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const documents = await _find({ id: req.params.id });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to insert review
app.post('/insert_review', raw({ type: '*/*' }), async (req, res) => {
    const data = JSON.parse(req.body);
    const documents = await find().sort({ id: -1 });
    let new_id = documents[0].id + 1; // Changed from ['id'] to .id

    const review = new Reviews({
        id: new_id,
        name: data.name, // Changed from ['name'] to .name
        dealership: data.dealership, // Changed from ['dealership'] to .dealership
        review: data.review, // Changed from ['review'] to .review
        purchase: data.purchase, // Changed from ['purchase'] to .purchase
        purchase_date: data.purchase_date, // Changed from ['purchase_date'] to .purchase_date
        car_make: data.car_make, // Changed from ['car_make'] to .car_make
        car_model: data.car_model, // Changed from ['car_model'] to .car_model
        car_year: data.car_year, // Changed from ['car_year'] to .car_year
    });

    try {
        const savedReview = await review.save();
        res.json(savedReview);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
