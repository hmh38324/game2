// 每日限制功能验证脚本
console.log('🎯 开始验证每日限制功能...');

// 模拟DailyLimitManager类
class DailyLimitManager {
    constructor() {
        this.gameId = 'game2';
        this.storageKey = 'daily_limit_data';
    }

    getChinaToday() {
        const now = new Date();
        const chinaTime = new Intl.DateTimeFormat('en-CA', {
            timeZone: 'Asia/Shanghai',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        }).format(now);
        return chinaTime;
    }

    getUserKey(employeeId, employeeName) {
        return `${employeeId}_${employeeName}`;
    }

    getData() {
        try {
            const data = localStorage.getItem(this.storageKey);
            const parsed = data ? JSON.parse(data) : { users: {} };
            
            if (!parsed.users || typeof parsed.users !== 'object') {
                return { users: {} };
            }
            
            return parsed;
        } catch (error) {
            console.error('获取本地数据失败:', error);
            return { users: {} };
        }
    }

    saveData(data) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('保存本地数据失败:', error);
            return false;
        }
    }

    checkDailyLimit(employeeId, employeeName) {
        const userKey = this.getUserKey(employeeId, employeeName);
        const today = this.getChinaToday();
        
        try {
            const data = this.getData();
            const user = data.users[userKey];
            
            if (user && user.lastPlayDate === today) {
                return {
                    canPlay: false,
                    reason: '今日已玩过游戏，请明天00:00后再试！',
                    playedGames: user.games || {}
                };
            }
            
            return { canPlay: true };
        } catch (error) {
            console.error('检查每日限制失败:', error);
            return { canPlay: true };
        }
    }

    recordGamePlay(employeeId, employeeName) {
        const userKey = this.getUserKey(employeeId, employeeName);
        const today = this.getChinaToday();
        
        try {
            const data = this.getData();
            
            if (!data.users[userKey]) {
                data.users[userKey] = {
                    lastPlayDate: today,
                    games: {}
                };
            }
            
            data.users[userKey].lastPlayDate = today;
            data.users[userKey].games[this.gameId] = true;
            
            const success = this.saveData(data);
            return success;
        } catch (error) {
            console.error('记录游戏失败:', error);
            return false;
        }
    }
}

// 测试函数
function runTests() {
    const manager = new DailyLimitManager();
    const testEmployeeId = '12345';
    const testEmployeeName = '测试用户';
    
    console.log('📅 当前中国时区日期:', manager.getChinaToday());
    console.log('👤 测试用户标识:', manager.getUserKey(testEmployeeId, testEmployeeName));
    
    // 清空测试数据
    localStorage.removeItem(manager.storageKey);
    console.log('🧹 清空测试数据');
    
    // 测试1: 第一次检查应该允许
    console.log('\n🔍 测试1: 第一次检查每日限制');
    const check1 = manager.checkDailyLimit(testEmployeeId, testEmployeeName);
    console.log('结果:', check1.canPlay ? '✅ 允许游戏' : '❌ 不允许游戏');
    
    // 测试2: 记录游戏
    console.log('\n💾 测试2: 记录游戏');
    const record = manager.recordGamePlay(testEmployeeId, testEmployeeName);
    console.log('结果:', record ? '✅ 记录成功' : '❌ 记录失败');
    
    // 测试3: 记录后检查应该限制
    console.log('\n🔍 测试3: 记录后检查每日限制');
    const check2 = manager.checkDailyLimit(testEmployeeId, testEmployeeName);
    console.log('结果:', check2.canPlay ? '❌ 应该被限制' : '✅ 正确被限制');
    if (!check2.canPlay) {
        console.log('限制原因:', check2.reason);
    }
    
    // 测试4: 验证数据
    console.log('\n📊 测试4: 验证存储数据');
    const data = manager.getData();
    const userKey = manager.getUserKey(testEmployeeId, testEmployeeName);
    const user = data.users[userKey];
    console.log('用户数据:', user ? '✅ 存在' : '❌ 不存在');
    if (user) {
        console.log('最后游戏日期:', user.lastPlayDate);
        console.log('已玩游戏:', user.games);
    }
    
    // 测试5: 时区测试
    console.log('\n🌏 测试5: 时区计算');
    const now = new Date();
    const chinaTime = manager.getChinaToday();
    const localTime = now.toISOString().split('T')[0];
    console.log('本地时间:', localTime);
    console.log('中国时区:', chinaTime);
    console.log('时区差异:', chinaTime !== localTime ? '存在差异' : '无差异');
    
    // 总结
    const allTestsPassed = check1.canPlay && record && !check2.canPlay && user;
    console.log('\n🎯 测试总结:', allTestsPassed ? '✅ 所有测试通过' : '❌ 存在问题');
    
    return allTestsPassed;
}

// 在浏览器环境中运行测试
if (typeof window !== 'undefined') {
    // 浏览器环境
    console.log('🌐 在浏览器环境中运行测试...');
    runTests();
} else {
    // Node.js环境
    console.log('🖥️ 在Node.js环境中运行测试...');
    console.log('注意: 此脚本需要在浏览器环境中运行以测试localStorage功能');
    console.log('请在浏览器控制台中运行: runTests()');
}
