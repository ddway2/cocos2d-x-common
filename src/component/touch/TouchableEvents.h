/*
 * Notifications.h
 *
 *  Created on: Jan 24, 2015
 *      Author: dawid
 */

#pragma once

#include <type_traits>
#include <functional>

#include <Notification.h>
#include <EventCollector.h>
#include <component/ComponentManager.h>

namespace cocos2d
{
class Touch;
}

namespace Dexode
{
namespace Component
{

MAKE_NOTIFICATION(TouchBegan, cocos2d::Touch*);

MAKE_NOTIFICATION(TouchMoved, cocos2d::Touch*);

MAKE_NOTIFICATION(TouchEnded, cocos2d::Touch*);

template<typename T>
struct has_onTouchBegan
{
private:
	template<typename U>
	static auto test(int, cocos2d::Touch* touch) -> decltype(std::declval<U>().onTouchBegan(touch), std::true_type{});

	template<typename>
	static std::false_type test(...);

public:
	static const bool value = std::is_same<decltype(test<T>(0, nullptr)), std::true_type>::value;
};

template<typename T>
typename std::enable_if<has_onTouchBegan<T>::value, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchBegan(T* value)
{
	return [=](cocos2d::Touch* touch)
	{
		value->onTouchBegan(touch);
	};
}

template<typename T>
typename std::enable_if<has_onTouchBegan<T>::value == false, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchBegan(T* value)
{
	return {};
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

template<typename T>
struct has_onTouchEnded
{
private:
	template<typename U>
	static auto test(int, cocos2d::Touch* touch) -> decltype(std::declval<U>().onTouchEnded(touch), std::true_type{});

	template<typename>
	static std::false_type test(...);

public:
	static const bool value = std::is_same<decltype(test<T>(0, nullptr)), std::true_type>::value;
};

template<typename T>
typename std::enable_if<has_onTouchEnded<T>::value, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchEnded(T* value)
{
	return [=](cocos2d::Touch* touch)
	{
		value->onTouchEnded(touch);
	};
}

template<typename T>
typename std::enable_if<has_onTouchEnded<T>::value == false, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchEnded(T* value)
{
	return {};
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

template<typename T>
struct has_onTouchMoved
{
private:
	template<typename U>
	static auto test(int, cocos2d::Touch* touch) -> decltype(std::declval<U>().onTouchMoved(touch), std::true_type{});

	template<typename>
	static std::false_type test(...);

public:
	static const bool value = std::is_same<decltype(test<T>(0, nullptr)), std::true_type>::value;
};

template<typename T>
typename std::enable_if<has_onTouchMoved<T>::value, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchMoved(T* value)
{
	return [=](cocos2d::Touch* touch)
	{
		value->onTouchMoved(touch);
	};
}

template<typename T>
typename std::enable_if<has_onTouchMoved<T>::value == false, std::function<void(cocos2d::Touch* touch)>>::type
get_onTouchMoved(T* value)
{
	return {};
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

template<class T>
EventCollector listenForTouches(T* component)
{
	static_assert(std::is_base_of<Base, T>::value, "T must inherit from Base component");
	EventCollector collector{component->getOwner()->getBus()};
	collector.listen(getNotificationTouchBegan(), get_onTouchBegan(component));
	collector.listen(getNotificationTouchMoved(), get_onTouchMoved(component));
	collector.listen(getNotificationTouchEnded(), get_onTouchEnded(component));

	return collector;
}

}
}
