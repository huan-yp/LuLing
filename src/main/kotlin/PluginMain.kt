package org.example.mirai.plugin

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.jsonObject
import net.mamoe.mirai.console.permission.AbstractPermitteeId
import net.mamoe.mirai.console.permission.PermissionService
import net.mamoe.mirai.console.permission.PermissionService.Companion.hasPermission
import net.mamoe.mirai.console.plugin.jvm.JvmPluginDescription
import net.mamoe.mirai.console.plugin.jvm.KotlinPlugin
import net.mamoe.mirai.contact.Member
import net.mamoe.mirai.contact.User
import net.mamoe.mirai.event.GlobalEventChannel
import net.mamoe.mirai.event.events.BotInvitedJoinGroupRequestEvent
import net.mamoe.mirai.event.events.FriendMessageEvent
import net.mamoe.mirai.event.events.GroupMessageEvent
import net.mamoe.mirai.event.events.NewFriendRequestEvent
import net.mamoe.mirai.message.data.buildMessageChain
import net.mamoe.mirai.message.data.Image
import net.mamoe.mirai.message.data.Image.Key.queryUrl
import net.mamoe.mirai.message.data.PlainText
import net.mamoe.mirai.utils.info
import net.mamoe.mirai.message.data.At
import net.mamoe.mirai.Bot
import net.mamoe.mirai.message.data.MessageSource.Key.quote


import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.*

/**
 * 使用 kotlin 版请把
 * `src/main/resources/META-INF.services/net.mamoe.mirai.console.plugin.jvm.JvmPlugin`
 * 文件内容改成 `org.example.mirai.plugin.PluginMain` 也就是当前主类全类名
 *
 * 使用 kotlin 可以把 java 源集删除不会对项目有影响
 *
 * 在 `settings.gradle.kts` 里改构建的插件名称、依赖库和插件版本
 *
 * 在该示例下的 [JvmPluginDescription] 修改插件名称，id和版本，etc
 *
 * 可以使用 `src/test/kotlin/RunMirai.kt` 在 ide 里直接调试，
 * 不用复制到 mirai-console-loader 或其他启动器中调试
 */
const val PORT = 1145
const val HOST = "127.0.0.1"
const val BotIdString = "1558718963"

object PluginMain : KotlinPlugin(
    JvmPluginDescription(
        id = "org.example.mirai-example",
        name = "鹿灵AI",
        version = "0.1.0"
    ) {
        author("幻影彭(3051561876@qq.com)")
        info(
            """
            使用自制接口连接 beta.character.ai, 实现的一个对话机器人 
        """.trimIndent()
        )
        // author 和 info 可以删除.
    }
) {
    override fun onEnable() {
        logger.info { "Plugin loaded" }
        //配置文件目录 "${dataFolder.absolutePath}/"
        val eventChannel = GlobalEventChannel.parentScope(this)
        eventChannel.subscribeAlways<GroupMessageEvent> {
//            群消息
//            复读示例
//            if (message.contentToString().startsWith("复读")) {
//                group.sendMessage(message.contentToString().replace("复读", ""))
//            }
//            分类示例
            val message_text = message.contentToString()
            var response :Map<String, JsonElement>
            var contentWithoutId = message_text.replace("@${BotIdString}", "")
            if (message_text.contains(bot.id.toString()) && contentWithoutId.length > 0) {
                var response_text = " LocalServer Offline! With Error:";
                try {
                    Socket(HOST, PORT).use { socket ->
                        val buffIn = BufferedReader(InputStreamReader(socket.getInputStream(), Charsets.UTF_8))
                        val buffOut = BufferedWriter(OutputStreamWriter(socket.getOutputStream(), Charsets.UTF_8))
                        val map_obj = mapOf("user" to sender.id.toString(), "text" to sender.nick + ":" + contentWithoutId)
                        buffOut.write(Json.encodeToString(map_obj))
                        buffOut.flush()
                        response = Json.parseToJsonElement(buffIn.readText()).jsonObject.toMap()
                    }
                    response_text = response["text"].toString()
                }
                catch (e:Throwable){
                    response_text += e.toString()
                }
                 response_text = response_text.substring(1, response_text.length)
                if(response_text.isNotEmpty()) {
                    response_text = response_text.replace("\\n", "\n")
                    val chain = buildMessageChain {
                        +message.quote()
                        +PlainText(response_text)
                    }
                    group.sendMessage(chain)
                }
            }
            message.forEach {
//                循环每个元素在消息里
                if (it is Image) {
                    //如果消息这一部分是图片
                    val url = it.queryUrl()
                    println(url)
//                    group.sendMessage("图片，下载地址$url")
                }
                if (it is PlainText) {
                    //如果消息这一部分是纯文本
//                    group.sendMessage("纯文本，内容:${it.content}")
                }
            }
        }
        eventChannel.subscribeAlways<FriendMessageEvent> {
            //好友信息
//            sender.sendMessage("hi")
        }
        eventChannel.subscribeAlways<NewFriendRequestEvent> {
            //自动同意好友申请
            accept()
        }
        eventChannel.subscribeAlways<BotInvitedJoinGroupRequestEvent> {
            //自动同意加群申请
            accept()
        }

        myCustomPermission // 注册权限
    }

    // region console 权限系统示例
    private val myCustomPermission by lazy { // Lazy: Lazy 是必须的, console 不允许提前访问权限系统
        // 注册一条权限节点 org.example.mirai-example:my-permission
        // 并以 org.example.mirai-example:* 为父节点

        // @param: parent: 父权限
        //                 在 Console 内置权限系统中, 如果某人拥有父权限
        //                 那么意味着此人也拥有该权限 (org.example.mirai-example:my-permission)
        // @func: PermissionIdNamespace.permissionId: 根据插件 id 确定一条权限 id
        PermissionService.INSTANCE.register(permissionId("my-permission"), "一条自定义权限", parentPermission)
    }

    public fun hasCustomPermission(sender: User): Boolean {
        return when (sender) {
            is Member -> AbstractPermitteeId.ExactMember(sender.group.id, sender.id)
            else -> AbstractPermitteeId.ExactUser(sender.id)
        }.hasPermission(myCustomPermission)
    }
    // endregion
}
