require('dotenv').config();
const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

// Worker URL ကို သန့်စင်ခြင်း
const WORKER_URL = process.env.WORKER_URL ? (process.env.WORKER_URL.endsWith('/') ? process.env.WORKER_URL : process.env.WORKER_URL + '/') : "";

bot.on(['video', 'document'], async (ctx) => {
    const file = ctx.message.video || ctx.message.document;
    let statusMsg;

    try {
        statusMsg = await ctx.reply('⏳ **Processing...**', { reply_to_message_id: ctx.message.message_id });
        
        // Telegram ဆီမှ Direct File Link ကို တောင်းယူခြင်း
        const fileLink = await ctx.telegram.getFileLink(file.file_id);
        
        // Link ထဲမှ filePath အပိုင်းကို ထုတ်ယူခြင်း
        const filePath = fileLink.href.split('/file/bot' + process.env.BOT_TOKEN + '/')[1];
        
        // Worker Link ထုတ်ပေးခြင်း
        const streamLink = `${WORKER_URL}${file.file_id}?path=${filePath}`;

        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, 
            `🎬 **Link Generated Successfully!**\n\n🔗 \`${streamLink}\`\n\n💡 *Use this link in VLC or MX Player.*`, 
            { parse_mode: 'Markdown' });

    } catch (e) {
        console.error("❌ Error:", e.message);
        if (statusMsg) {
            await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, "❌ Error generating link. Please try again.");
        }
    }
});

bot.launch().then(() => {
    console.log("🚀 Bot is running perfectly!");
});

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
