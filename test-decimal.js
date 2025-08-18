// Decimal型のテスト
const mockGoals = [
  {achievement_status: 'in_progress', progress_rate: {toString: () => '0'}, achievement_rate: {toString: () => '0'}},
  {achievement_status: 'completed', progress_rate: {toString: () => '100'}, achievement_rate: {toString: () => '100'}},
  {achievement_status: 'completed', progress_rate: {toString: () => '100'}, achievement_rate: null},
  {achievement_status: 'in_progress', progress_rate: {toString: () => '0'}, achievement_rate: null},
  {achievement_status: 'NOT_STARTED', progress_rate: null, achievement_rate: null},
  {achievement_status: 'NOT_STARTED', progress_rate: null, achievement_rate: null}
];

// 修正後のロジック
let totalProgress = 0;
let activeGoalCount = mockGoals.length;

mockGoals.forEach((goal) => {
  if (goal.achievement_status === 'completed' || goal.achievement_status === 'achieved') {
    totalProgress += 100;
  } else {
    let progressValue = 0;
    if (goal.progress_rate !== null && goal.progress_rate !== undefined) {
      progressValue = typeof goal.progress_rate === 'object' 
        ? parseFloat(goal.progress_rate.toString()) 
        : Number(goal.progress_rate);
    } else if (goal.achievement_rate !== null && goal.achievement_rate !== undefined) {
      progressValue = typeof goal.achievement_rate === 'object'
        ? parseFloat(goal.achievement_rate.toString())
        : Number(goal.achievement_rate);
    }
    totalProgress += progressValue;
  }
});

const overallProgress = activeGoalCount > 0 
  ? totalProgress / activeGoalCount 
  : 0;

console.log('総進捗: ' + totalProgress);
console.log('目標数: ' + activeGoalCount);
console.log('目標達成率: ' + Math.round(overallProgress) + '%');
