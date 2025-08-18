// 000001のデータで計算テスト
const goals = [
  {status: 'in_progress', progress: 0},
  {status: 'postponed', progress: 0},
  {status: 'cancelled', progress: 50},
  {status: 'completed', progress: 100},
  {status: 'completed', progress: 100},
  {status: 'in_progress', progress: 0},
  {status: 'NOT_STARTED', progress: 0},
  {status: 'NOT_STARTED', progress: 0}
];

// 修正前のロジック
function oldCalc(goals) {
  const currentGoals = goals.filter(g => g.status === 'in_progress' || g.status === 'pending');
  const completedGoals = goals.filter(g => g.status === 'completed' || g.status === 'achieved');
  
  let totalProgress = 0;
  let totalGoalCount = goals.length;
  
  totalProgress += completedGoals.length * 100;
  totalProgress += currentGoals.reduce((sum, goal) => sum + goal.progress, 0);
  
  return totalGoalCount > 0 ? totalProgress / totalGoalCount : 0;
}

// 修正後のロジック
function newCalc(goals) {
  const activeGoals = goals.filter(g => 
    g.status !== 'cancelled' && g.status !== 'postponed'
  );
  
  let totalProgress = 0;
  let activeGoalCount = activeGoals.length;
  
  activeGoals.forEach(goal => {
    if (goal.status === 'completed' || goal.status === 'achieved') {
      totalProgress += 100;
    } else {
      totalProgress += goal.progress;
    }
  });
  
  return activeGoalCount > 0 ? totalProgress / activeGoalCount : 0;
}

console.log('旧計算: ' + Math.round(oldCalc(goals)) + '%');
console.log('新計算: ' + Math.round(newCalc(goals)) + '%');
