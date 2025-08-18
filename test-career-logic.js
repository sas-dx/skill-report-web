// 000001のデータで計算テスト（キャリアプラン方式）
const mockGoals = [
  {status: 'in_progress', progress_rate: {toString: () => '0'}},
  {status: 'postponed', progress_rate: {toString: () => '0'}},
  {status: 'cancelled', progress_rate: {toString: () => '50'}},
  {status: 'completed', progress_rate: {toString: () => '100'}},
  {status: 'completed', progress_rate: {toString: () => '100'}},
  {status: 'in_progress', progress_rate: {toString: () => '0'}},
  {status: 'NOT_STARTED', progress_rate: null},
  {status: 'NOT_STARTED', progress_rate: null}
];

// キャリアプラン方式の計算
let totalProgress = 0;

mockGoals.forEach((goal) => {
  let progressValue = 0;
  if (goal.progress_rate !== null && goal.progress_rate !== undefined) {
    progressValue = typeof goal.progress_rate === 'object' 
      ? parseFloat(goal.progress_rate.toString()) 
      : Number(goal.progress_rate);
  }
  totalProgress += progressValue;
});

const overallProgress = mockGoals.length > 0 
  ? totalProgress / mockGoals.length 
  : 0;

console.log('総進捗: ' + totalProgress);
console.log('目標数: ' + mockGoals.length);
console.log('目標達成率（キャリアプラン方式）: ' + Math.round(overallProgress) + '%');
