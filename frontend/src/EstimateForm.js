import { useState, useEffect } from "react";

// TODO: Replace this with your actual token or later implement login to get it dynamically
const USER_TOKEN = "686e5863b356d6d970e6cd1ab3f52d568a4d3399";

function EstimateForm() {
    const [squareFootage, setSquareFootage] = useState("");
    const [poundEstimate, setPoundEstimate] = useState("");
    const [crewSize, setCrewSize] = useState("");
    const [price, setPrice] = useState(null);
    const [estimates, setEstimates] = useState([]);
    const [error, setError] = useState("");

    // Fetch all estimates for this user
    const fetchEstimates = async () => {
        setError("");
        try {
            const response = await fetch("http://localhost:8000/api/estimates/", {
                method: "GET",
                headers: {
                    "Authorization": `Token ${USER_TOKEN}`,
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data = await response.json();
                setEstimates(data);
            } else if (response.status === 401 || response.status === 403) {
                setError("Authentication required. Invalid token.");
            } else {
                setError("Failed to fetch estimates.");
            }
        } catch (err) {
            setError("Network error: Could not fetch estimates.");
        }
    };

    useEffect(() => {
        fetchEstimates();
    }, []);

    // Handle creating a new estimate
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const response = await fetch("http://localhost:8000/api/estimates/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Token ${USER_TOKEN}`,
                },
                body: JSON.stringify({
                    square_footage: Number(squareFootage),
                    pound_estimate: Number(poundEstimate),
                    crew_size: Number(crewSize),
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setPrice(data.price);
                fetchEstimates(); // refresh list
                setSquareFootage("");
                setPoundEstimate("");
                setCrewSize("");
            } else if (response.status === 400) {
                const data = await response.json();
                setError("Invalid input: " + JSON.stringify(data));
            } else if (response.status === 401 || response.status === 403) {
                setError("Authentication required. Invalid token.");
            } else {
                setError("Failed to create estimate.");
            }
        } catch (err) {
            setError("Network error: Could not create estimate.");
        }
    };

    return (
        <div>
            <h2>Moving Cost Estimator</h2>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Square Footage:</label>
                    <input
                        type="number"
                        value={squareFootage}
                        onChange={(e) => setSquareFootage(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Pound Estimate:</label>
                    <input
                        type="number"
                        value={poundEstimate}
                        onChange={(e) => setPoundEstimate(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Crew Size:</label>
                    <input
                        type="number"
                        value={crewSize}
                        onChange={(e) => setCrewSize(e.target.value)}
                        required
                    />
                </div>

                <button type="submit">Get Estimate</button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}
            {price && <h3>Estimated Price: ${price}</h3>}

            <h3>My Estimates</h3>
            <ul>
                {estimates.map((estimate) => (
                    <li key={estimate.id}>
                        {estimate.square_footage} sqft, {estimate.pound_estimate} lbs, Crew: {estimate.crew_size}, Price: ${estimate.price}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EstimateForm;
