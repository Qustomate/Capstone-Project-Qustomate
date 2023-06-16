package com.qustomate.main_page;

import okhttp3.*;
import org.json.*;

import java.io.IOException;

public class LoginManager {
    private static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    private OkHttpClient client;

    public LoginManager() {
        client = new OkHttpClient();
    }

    public void performLogin(String email, String password) {
        try {
            JSONObject requestBody = new JSONObject();
            requestBody.put("email", email);
            requestBody.put("password", password);

            RequestBody body = RequestBody.create(JSON, requestBody.toString());

            Request request = new Request.Builder()
                    .url("https://qustomate.et.r.appspot.com/auth/login")
                    .post(body)
                    .build();

            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    e.printStackTrace();
                    // Handle network or API call failure
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (response.isSuccessful()) {
                        // Handle successful login
                        String responseData = response.body().string();
                        try {
                            JSONObject jsonResponse = new JSONObject(responseData);
                            // Parse the response data and extract relevant information
                            // Example:
                            String authToken = jsonResponse.getString("auth_token");
                            int userId = jsonResponse.getInt("user_id");
                            // Use the obtained information for further actions
                        } catch (JSONException e) {
                            e.printStackTrace();
                            // Handle JSON parsing error
                        }
                    } else {
                        // Handle unsuccessful login
                        // Example: display an error message to the user
                        System.out.println("Login failed. Please check your credentials.");
                    }
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
            // Handle JSON creation error
        }
    }
}
