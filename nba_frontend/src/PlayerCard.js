function PlayerCard( { playerId, data}) {
    return (
        <div style = {{
            display: "flex",
            alignItems: "center",
            border: "2px solid #000",
            borderRadius: "8px",
            padding: "20px",
            width: "400px",
            backgroundColor: "#f9f9f9"
        }}>
            <img
              src={`https://cdn.nba.com/headshots/nba/latest/260x190/${playerId}.png`}
              alt={`${data.player_name}`}
              style={{ width: "120px", height: "90px", marginRight: "20px" }}
            />
            <div>
                <h2 style={{ margin: " 0 0 8px 0"}}>{data.player_name}</h2>
                <p><strong>Career Averages</strong></p>
                <p>PPG: {data.career_average.PPG}</p>
                <p>APG: {data.career_average.APG}</p>
                <p>RPG: {data.career_average.RPG}</p>
                <p>SPG: {data.career_average.SPG}</p>
                <p>BPG: {data.career_average.BPG}</p>
            </div>
        </div>
    );
}
export default PlayerCard;