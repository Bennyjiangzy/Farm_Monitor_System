import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [status, setStatus] = useState({});
    const [error, setError] = useState(null)

	const getStatus = () => {
	
        fetch(`http://benny-3855-lab.westeurope.cloudapp.azure.com:8120/status`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Status")
                setStatus(result);
                setIsLoaded(true);
            },(error) =>{
                console.log(error)
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStatus(), 10000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStatus]);

    

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        let oldtime = status['last_update'].replace("T", " ").replace("Z", " ");
        console.log(oldtime)
        console.log(new Date())
        let time = Math.round((new Date().getTime() - new Date(oldtime).getTime() + 8*60*60) / 1000)
        // console.log(new Date().
        return(
            <div>
                <h1>Service status</h1>
                <table className={"StatsTable"}>
					<tbody align="left">
						<tr>
							<td colspan="2"><span class="names">Receiver: </span>{status['receiver']}</td>
                        </tr>

                        <tr>
							<td colspan="2"><span class="names">Storage: </span>{status['storage']}</td>
                        </tr>

                        <tr>
							<td colspan="2"><span class="names">Processing: </span>{status['processing']}</td>
                        </tr>

                        <tr>
							<td colspan="2"><span class="names">Audit: </span>{status['audit']}</td>
                        </tr>

                        <tr>
							<td colspan="2"><span class="names">Last Update: </span>{time} seconds ago</td>
						</tr>
					</tbody>
                </table>
            </div>
        )
    }
}
