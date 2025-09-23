import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
function PlayerComparison({player1, player2}) {
    const compare_data = [
        {
            stat: "PPG",
            [player1.player_name]: player1.career_average.PPG,
            [player2.player_name]: player2.career_average.PPG
        },
        {
            stat: "APG",
            [player1.player_name]: player1.career_average.APG,
            [player2.player_name]: player2.career_average.APG
        },
        {
            stat: "RPG",
            [player1.player_name]: player1.career_average.RPG,
            [player2.player_name]: player2.career_average.RPG
        },
        {
            stat: "SPG",
            [player1.player_name]: player1.career_average.SPG,
            [player2.player_name]: player2.career_average.SPG
        },
        {
            stat: "BPG",
            [player1.player_name]: player1.career_average.BPG,
            [player2.player_name]: player2.career_average.BPG
        },
    ];
    return (
        <ResponsiveContainer width="100%" height={400}>
      <BarChart data={compare_data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="stat" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey={player1.player_name} fill="#8884d8" />
        <Bar dataKey={player2.player_name} fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
    )
}
export default PlayerComparison