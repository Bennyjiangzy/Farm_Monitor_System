import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://benny-3855-lab.westeurope.cloudapp.azure.com:8110:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                console.log(error)
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Average temperature</th>
							<th>Average water use</th>
						</tr>
						<tr>
							<td># Env: {stats['avg_env_temp_reading']}</td>
							<td># Water: {stats['avg_res_water_reading']}</td>
						</tr>
						<tr>
							<td colspan="2">Max temperature: {stats['max_env_temp_reading']}</td>
						</tr>
						<tr>
							<td colspan="2">Max water Usage: {stats['max_res_water_reading']}</td>
						</tr>
						<tr>
							<td colspan="2">Avg power: {stats['avg_res_elerity_reading']}</td>
						</tr>
						<tr>
							<td colspan="2">Avg humidity: {stats['avg_env_humidity_reading']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
