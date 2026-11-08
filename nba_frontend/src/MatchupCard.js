const NBA_TEAM_IDS = {
  ATL: "1610612737",
  BOS: "1610612738",
  BKN: "1610612751",
  CHA: "1610612766",
  CHI: "1610612741",
  CLE: "1610612739",
  DAL: "1610612742",
  DEN: "1610612743",
  DET: "1610612765",
  GSW: "1610612744",
  HOU: "1610612745",
  IND: "1610612754",
  LAC: "1610612746",
  LAL: "1610612747",
  MEM: "1610612763",
  MIA: "1610612748",
  MIL: "1610612749",
  MIN: "1610612750",
  NO: "1610612740",
  NOP: "1610612740",
  NYK: "1610612752",
  OKC: "1610612760",
  ORL: "1610612753",
  PHI: "1610612755",
  PHX: "1610612756",
  POR: "1610612757",
  SAC: "1610612758",
  SAS: "1610612759",
  TOR: "1610612761",
  UTA: "1610612762",
  UTAH: "1610612762",
  WAS: "1610612764",
};

function MatchupCard({ game }) {
  const isScheduled = game["Status"] === "Scheduled";
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        border: "1px solid #ddd",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        borderRadius: "12px",
        padding: "15px 20px",
        width: "500px",
        backgroundColor: "#f9f9f9",
        margin: "15px auto",
      }}
    >
      {/* Top Row: Away vs Home Logos */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        {/* Away Team */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "6px",
            width: "100px",
          }}
        >
          <strong>{game["Away Team"]}</strong>
          <img
            src={`https://cdn.nba.com/logos/nba/${NBA_TEAM_IDS[game["Away Team"]]}/primary/L/logo.svg`}
            alt={`${game["Away Team"]} Logo`}
            style={{ width: "60px", height: "60px", objectFit: "contain" }}
          />
          <span style={{ fontSize: "0.85rem", color: "#666" }}>
          {game["Away Record"]}
        </span>
        </div>

        {/* Score / VS */}
        <div
          style={{
            fontWeight: "bold",
            fontSize: "1.4rem",
            color: "#333",
            textAlign: "center",
          }}
        >
          {isScheduled
            ? "VS"
            : `${game["Away Score"]} - ${game["Home Score"]}`}
        </div>

        {/* Home Team */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "6px",
            width: "100px",
          }}
        >
          <strong>{game["Home Team"]}</strong>
          <img
            src={`https://cdn.nba.com/logos/nba/${NBA_TEAM_IDS[game["Home Team"]]}/primary/L/logo.svg`}
            alt={`${game["Home Team"]} Logo`}
            style={{ width: "60px", height: "60px", objectFit: "contain" }}
          />
          <span style={{ fontSize: "0.85rem", color: "#666" }}>
          {game["Home Record"]}
        </span>
        </div>
      </div>

<div style={{ textAlign: "center", marginTop: "12px" }}>
  <p style={{ margin: "3px 0", fontWeight: "bold" }}>
    {new Date(game["Game Time"]).toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      timeZone: "America/New_York",
      timeZoneName: "short",
    })}
  </p>

  <p style={{ margin: "3px 0", color: "#555" }}>
    {game["Arena"]}
  </p>
        <p
          style={{
            margin: "3px 0",
            fontWeight: "bold",
            color:
              game["Status"].includes("Final")
                ? "#D62828"
                : game["Status"].includes("In Progress")
                ? "#2A9D8F"
                : "#6c757d",
          }}
        >
          {game["Status"]}
        </p>

        {/* Quarter and Time Remaining */}
        {game["Status"] === "In Progress" && (
          <p
            style={{
              margin: "5px 0",
              fontWeight: "bold",
              color: "#2A9D8F",
            }}
          >
            {game["Quarter"] <= 4
              ? `Q${game["Quarter"]}`
              : `OT${game["Quarter"] - 4}`}{" "}
            • {game["Clock"]} remaining
          </p>
        )}
      </div>
    </div>
  );
}

export default MatchupCard;
