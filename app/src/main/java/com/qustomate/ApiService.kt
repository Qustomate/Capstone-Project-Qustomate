package com.qustomate

import com.google.gson.GsonBuilder
import com.google.gson.InstanceCreator
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.logging.HttpLoggingInterceptor
import okio.Timeout
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Url
import java.lang.reflect.Type

class CallInstanceCreator<T> : InstanceCreator<Call<T>> {
    override fun createInstance(type: Type): Call<T> {
        return object : Call<T> {
            // Implement the required methods of the Call interface.
            // You can delegate these methods to another Call instance or provide dummy implementations if necessary.

            override fun enqueue(callback: Callback<T>) {
                // Handle enqueue logic if needed
            }

            override fun isExecuted(): Boolean {
                // Handle isExecuted logic if needed
                return false
            }

            override fun clone(): Call<T> {
                // Handle clone logic if needed
                return this
            }

            override fun isCanceled(): Boolean {
                // Handle isCanceled logic if needed
                return false
            }

            override fun request(): Request {
                TODO("Not yet implemented")
            }

            override fun timeout(): Timeout {
                TODO("Not yet implemented")
            }

            override fun cancel() {
                // Handle cancel logic if needed
            }

            override fun execute(): retrofit2.Response<T> {
                // Handle execute logic if needed
                throw UnsupportedOperationException("execute() is not supported.")
            }

            // You can add more methods based on your requirements.
        }
    }
}

val gson = GsonBuilder()
    .registerTypeAdapter(Call::class.java, CallInstanceCreator<Any>())
    .create()

interface ApiService {
    @POST("message/add")
    suspend fun addMessage(@Body message: CustomChatMessage): Boolean

    @GET
    suspend fun getContact(@Url url: String): List<Contact>

    @GET
    suspend fun getMessages(@Url url: String): List<CustomChatMessage>
}

data class CustomChatMessage(
    val id_message: String,
    val message_text: String,
    val recipientID: String,
    val sender_id: String,
    val time_stamp: String
)

data class Contact(
    val name: String,
    val phone: String,
    val email: String
)

object ApiClient {
    private const val BASE_URL = "https://qustomate.et.r.appspot.com/"

    fun create(): ApiService {
        val logger = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        val client = OkHttpClient.Builder()
            .addInterceptor(logger)
            .build()

        val gson = GsonBuilder()
            .registerTypeAdapter(Call::class.java, CallInstanceCreator<Any>())
            .create()

        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()

        return retrofit.create(ApiService::class.java)
    }
}

