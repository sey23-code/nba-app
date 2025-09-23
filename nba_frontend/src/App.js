import TeamsList from './TeamsList';
import {Routes, Route } from "react-router-dom"
import RosterList from './RosterList';
import PlayerStats from './PlayerStats';
import PlayerComparisonPage from './PlayerComparisonPage';
import './App.css';
function App() {
  return (
    <Routes>
      <Route path="/" element={<TeamsList />}/>
      <Route path="/team/:teamId" element={<RosterList />}/>
      <Route path="/player/:playerId" element={<PlayerStats />}></Route>
      <Route path="/compare" element={<PlayerComparisonPage />}></Route>
    </Routes>
  );
}

export default App;
